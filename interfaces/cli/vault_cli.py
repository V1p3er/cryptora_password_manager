import uuid
from dataclasses import dataclass

from rich.prompt import Prompt

from application.services.add_credential import AddCredentialService
from application.services.create_vault import CreateVaultService
from application.services.get_credential import GetCredentialService
from application.services.list_credentials import ListCredentialsService
from application.services.lock_vault import LockVaultService
from application.services.remove_credential import RemoveCredentialService
from application.services.unlock_vault import UnlockVaultService, VaultSessionStore
from application.services.update_credential import UpdateCredentialService
from domain.entities.user import User
from domain.services.password_strength_calculator import PasswordStrengthCalculator
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.domain_name import DomainName
from domain.value_objects.service_name import ServiceName
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.vault_item_username import VaultItemUsername
from infrastructure.config.settings import Settings
from infrastructure.crypto.argon2_key_derivation import Argon2KeyDerivation
from infrastructure.crypto.cryptography_encryption import CryptographyEncryption
from infrastructure.persistence.file_vault_repository import (
    FileStorage,
    FileUserRepository,
    FileVaultRepository,
)
from infrastructure.security.password_hasher import Argon2PasswordHasher, Argon2PasswordVerifier
from interfaces.cli.menu import (
    console,
    print_error,
    print_info,
    print_success,
    print_warning,
    render_header,
    render_main_menu,
)


CANCEL_TOKEN = "cancel"


@dataclass(slots=True)
class CliSession:
    current_user_id: UserId | None = None
    current_username: str | None = None
    current_master_password: MasterPassword | None = None


class VaultCLI:
    def __init__(self) -> None:
        settings = Settings.from_env()
        storage = FileStorage(settings.storage_file_path)

        self._user_repo = FileUserRepository(storage)
        self._vault_repo = FileVaultRepository(storage)
        self._sessions = VaultSessionStore()

        self._deriver = Argon2KeyDerivation()
        self._encryption = CryptographyEncryption()
        self._verifier = Argon2PasswordVerifier()

        self._create_vault = CreateVaultService(self._vault_repo)
        self._unlock_vault = UnlockVaultService(
            user_repository=self._user_repo,
            vault_repository=self._vault_repo,
            password_verifier=self._verifier,
            key_deriver=self._deriver,
            encryption_service=self._encryption,
            session_store=self._sessions,
        )
        self._lock_vault = LockVaultService(self._sessions)
        self._add_credential = AddCredentialService(self._vault_repo, self._encryption)
        self._list_credentials = ListCredentialsService(self._vault_repo, self._sessions)
        self._get_credential = GetCredentialService(self._vault_repo, self._sessions)
        self._update_credential = UpdateCredentialService(self._vault_repo, self._encryption)
        self._remove_credential = RemoveCredentialService(self._vault_repo)

        self._state = CliSession()

    def run(self) -> None:
        while True:
            console.clear()
            render_header(self._state.current_username)
            render_main_menu()
            choice = self._prompt_menu_choice()

            if choice == "0":
                print_info("Goodbye. Stay secure.")
                break

            handler = {
                "1": self._register_user,
                "2": self._login,
                "3": self._create_user_vault,
                "4": self._unlock_current_vault,
                "5": self._lock_current_vault,
                "6": self._add_credential_flow,
                "7": self._list_credentials_flow,
                "8": self._get_credential_flow,
                "9": self._update_credential_flow,
                "10": self._remove_credential_flow,
                "11": self._logout,
            }.get(choice)

            if handler is None:
                print_error("Invalid selection. Choose one of the menu numbers.")
                self._pause()
                continue

            try:
                handler()
            except Exception as exc:
                print_error(str(exc))
            self._pause()

    def _prompt_menu_choice(self) -> str:
        while True:
            choice = Prompt.ask("[bold]Select an action[/bold]").strip()
            if choice in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"}:
                return choice
            print_error("Invalid menu number. Please enter 0-11.")

    def _prompt_text(self, label: str, *, allow_empty: bool = False) -> str | None:
        hint = f"{label} [dim](or type '{CANCEL_TOKEN}')[/dim]"
        while True:
            value = Prompt.ask(hint).strip()
            if value.lower() == CANCEL_TOKEN:
                print_info("Operation cancelled.")
                return None
            if not value and not allow_empty:
                print_error(f"{label} cannot be empty.")
                continue
            return value

    def _prompt_validated(
        self,
        *,
        label: str,
        example: str,
        parser,
        allow_empty: bool = False,
    ):
        while True:
            value = self._prompt_text(f"{label} (example: {example})", allow_empty=allow_empty)
            if value is None:
                return None
            if allow_empty and value == "":
                return ""
            try:
                return parser(value)
            except Exception as exc:
                print_error(f"{label} is invalid: {exc}")

    def _prompt_master_password(self, label: str = "Master Password") -> MasterPassword | None:
        while True:
            raw = self._prompt_text(
                f"{label} (example: ValidPassw0rd!)"
            )
            if raw is None:
                return None
            try:
                return MasterPassword(raw)
            except Exception as exc:
                print_error(f"{exc}. Try again.")

    def _require_login(self) -> bool:
        if self._state.current_user_id is None:
            print_warning("You need to login first.")
            return False
        return True

    def _derive_user_key(self, user_id: UserId, mp: MasterPassword) -> bytes:
        salt = str(user_id.value).encode("utf-8")[:16]
        return self._deriver.derive_key(mp, salt)

    def _register_user(self) -> None:
        username = self._prompt_validated(
            label="Username",
            example="john_doe7",
            parser=lambda v: Username(v),
        )
        if username is None:
            return

        while True:
            password = self._prompt_master_password()
            if password is None:
                return
            confirm = self._prompt_text("Confirm Master Password")
            if confirm is None:
                return
            if confirm != password.value:
                print_error("Passwords do not match. Please try again.")
                continue
            break

        if self._user_repo.exists_by_username(username):
            raise ValueError("Username already exists.")

        strength = PasswordStrengthCalculator.calculate(password.value)
        if strength.is_weak():
            raise ValueError("Password is weak. Use stronger password.")

        user = User.create(
            user_id=UserId(uuid.uuid4()),
            username=username,
            password_hash=Argon2PasswordHasher.hash(password),
            created_at=CreatedAt.now(),
        )
        self._user_repo.save(user)
        print_success(f"User '{username.value}' registered.")

    def _login(self) -> None:
        username = self._prompt_validated(
            label="Username",
            example="john_doe7",
            parser=lambda v: Username(v),
        )
        if username is None:
            return
        password = self._prompt_master_password()
        if password is None:
            return

        user = self._user_repo.get_by_username(username)
        if user is None:
            raise ValueError("User not found.")
        if not self._verifier.verify(password, user.password_hash):
            raise ValueError("Invalid master password.")

        self._state.current_user_id = user.user_id
        self._state.current_username = user.username.value
        self._state.current_master_password = password
        print_success(f"Logged in as {user.username.value}.")

    def _create_user_vault(self) -> None:
        if not self._require_login():
            return
        dto = self._create_vault.execute(self._state.current_user_id)
        print_success(f"Vault created with ID {dto.vault_id}.")

    def _unlock_current_vault(self) -> None:
        if not self._require_login():
            return
        password = self._prompt_master_password()
        if password is None:
            return
        self._unlock_vault.execute(self._state.current_user_id, password)
        self._state.current_master_password = password
        print_success("Vault unlocked.")

    def _lock_current_vault(self) -> None:
        if not self._require_login():
            return
        self._lock_vault.execute(self._state.current_user_id)
        print_success("Vault locked.")

    def _add_credential_flow(self) -> None:
        if not self._require_login():
            return
        if self._state.current_master_password is None:
            raise ValueError("Login and unlock vault first.")

        title_vo = self._prompt_validated(
            label="Service Title",
            example="gmail",
            parser=lambda v: ServiceName(v),
        )
        if title_vo is None:
            return
        username_vo = self._prompt_validated(
            label="Credential Username",
            example="me.user",
            parser=lambda v: VaultItemUsername(v),
        )
        if username_vo is None:
            return
        domain_vo = self._prompt_validated(
            label="Domain",
            example="gmail.com",
            parser=lambda v: DomainName(v),
        )
        if domain_vo is None:
            return
        password = self._prompt_text("Credential Password (example: my-secret-pass)")
        if password is None:
            return

        key = self._derive_user_key(self._state.current_user_id, self._state.current_master_password)
        dto = self._add_credential.execute(
            user_id=self._state.current_user_id,
            password_key=key,
            password_plaintext=password,
            domain=domain_vo.value,
            title=title_vo.value,
            username=username_vo.value,
        )
        self._sessions.set_password(self._state.current_user_id, dto.item_id, dto.password)
        print_success(f"Credential added with ID {dto.item_id}.")

    def _list_credentials_flow(self) -> None:
        if not self._require_login():
            return
        items = self._list_credentials.execute(self._state.current_user_id)
        if not items:
            print_info("No credentials found.")
            return
        for item in items:
            console.print(
                f"[bold cyan]#{item.item_id}[/bold cyan] "
                f"{item.title or '-'} | {item.username or '-'} | {item.domain}"
            )

    def _get_credential_flow(self) -> None:
        if not self._require_login():
            return
        item_id = self._prompt_item_id()
        if item_id is None:
            return
        item = self._get_credential.execute(self._state.current_user_id, item_id)
        console.print(f"[bold]ID:[/bold] {item.item_id}")
        console.print(f"[bold]Title:[/bold] {item.title}")
        console.print(f"[bold]Username:[/bold] {item.username}")
        console.print(f"[bold]Domain:[/bold] {item.domain}")
        console.print(f"[bold green]Password:[/bold green] {item.password}")

    def _update_credential_flow(self) -> None:
        if not self._require_login():
            return
        if self._state.current_master_password is None:
            raise ValueError("Login and unlock vault first.")

        item_id = self._prompt_item_id()
        if item_id is None:
            return

        print_info("Leave field empty to keep current value.")
        new_title = self._prompt_validated(
            label="New Title",
            example="primary mail",
            parser=lambda v: ServiceName(v),
            allow_empty=True,
        )
        if new_title is None:
            return
        new_username = self._prompt_validated(
            label="New Username",
            example="me.work",
            parser=lambda v: VaultItemUsername(v),
            allow_empty=True,
        )
        if new_username is None:
            return
        new_domain = self._prompt_validated(
            label="New Domain",
            example="mail.google.com",
            parser=lambda v: DomainName(v),
            allow_empty=True,
        )
        if new_domain is None:
            return
        new_password = self._prompt_text(
            "New Password (example: N3wStrongPass!)", allow_empty=True
        )
        if new_password is None:
            return

        key = self._derive_user_key(self._state.current_user_id, self._state.current_master_password)
        dto = self._update_credential.execute(
            user_id=self._state.current_user_id,
            item_id=item_id,
            password_key=key,
            new_title=(new_title.value if new_title else None),
            new_username=(new_username.value if new_username else None),
            new_domain=(new_domain.value if new_domain else None),
            new_password_plaintext=new_password or None,
        )
        if new_password:
            self._sessions.set_password(self._state.current_user_id, item_id, new_password)
        print_success(f"Credential {dto.item_id} updated.")

    def _remove_credential_flow(self) -> None:
        if not self._require_login():
            return
        item_id = self._prompt_item_id()
        if item_id is None:
            return

        confirm = self._prompt_text("Type YES to confirm deletion")
        if confirm is None:
            return
        if confirm != "YES":
            print_warning("Deletion cancelled. You must type exactly YES.")
            return

        self._remove_credential.execute(self._state.current_user_id, item_id)
        print_success(f"Credential {item_id} removed.")

    def _logout(self) -> None:
        if self._state.current_user_id is not None:
            self._lock_vault.execute(self._state.current_user_id)
        self._state = CliSession()
        print_success("Logged out.")

    def _prompt_item_id(self) -> int | None:
        while True:
            raw = self._prompt_text("Credential ID")
            if raw is None:
                return None
            if not raw.isdigit():
                print_error("Credential ID must be a non-negative integer.")
                continue
            return int(raw)

    @staticmethod
    def _pause() -> None:
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
