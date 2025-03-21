
from bisq.asset.base58_address_validator import Base58AddressValidator
from bisq.asset.coin import Coin
from bisq.asset.network_parameters_adapter import NetworkParametersAdapter


class Myce(Coin):
    
    class MyceParams(NetworkParametersAdapter):
        def __init__(self):
            super().__init__()
            self.address_header = 50
            self.p2sh_header = 85
    
    def __init__(self):
        super().__init__(
            name="Myce",
            ticker_symbol="YCE",
            address_validator=Base58AddressValidator(self.MyceParams()),
        )
        