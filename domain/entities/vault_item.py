from dataclasses import dataclass

from domain.value_objects.service_name import ServiceName
from domain.value_objects.domain_name import DomainName
from domain.value_objects.username import Username
from domain.value_objects.encrypted_value import EncryptedValue


@dataclass
class VaultItem:
    service_name: ServiceName
    domain_name: DomainName
    username: Username
    encrypted_password: EncryptedValue
