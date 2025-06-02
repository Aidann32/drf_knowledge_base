from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from web3 import Web3

from .models import NFT
from .serializers import NFTSerializer
from config.settings import CONTRACT_ADDRESS, ABI, WEB3_HTTP_PROVIDER, PRIVATE_KEY


class MintNFTAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from web3 import Web3

from .models import NFT
from .serializers import NFTSerializer
from config.settings import CONTRACT_ADDRESS, ABI, WEB3_HTTP_PROVIDER, PRIVATE_KEY

class MintNFTAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        metadata_url = request.data.get("metadata_url")

        if not metadata_url:
            return Response(
                {"error": "Metadata URL is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Подключение к Web3
            w3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))
            current_gas_price = w3.eth.gas_price
            if not w3.is_connected():
                return Response(
                    {"error": "Failed to connect to the blockchain network."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Адрес отправителя
            sender_address = w3.eth.account.from_key(PRIVATE_KEY).address

            # Подключение к контракту
            contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

            # Получение nonce
            nonce = w3.eth.get_transaction_count(sender_address)

            # Создание транзакции
            transaction = contract.functions.mint(user.wallet_address, metadata_url).build_transaction({
                'chainId': 11155111,  # Chain ID для сети Sepolia
                'gas': 3000000,  # Лимит газа
                'gasPrice':  int(current_gas_price * 1.2),  # Цена газа
                'nonce': nonce,
            })

            # Подпись транзакции
            signed_tx = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)

            # Отправка транзакции
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # Правильное использование

            # Ожидание подтверждения
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            # Сохранение информации об NFT
            nft = NFT.objects.create(
                user=user,
                token_id=tx_receipt["logs"][0]["topics"][3].hex(),  # Получение токен ID из событий
                ipfs_hash=metadata_url.split("/")[-1],
                metadata_url=metadata_url,
            )
            serializer = NFTSerializer(nft)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserNFTListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        nfts = NFT.objects.filter(user=user)
        serializer = NFTSerializer(nfts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NFTDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token_id, *args, **kwargs):
        try:
            nft = NFT.objects.get(token_id=token_id)
            serializer = NFTSerializer(nft)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NFT.DoesNotExist:
            return Response({"error": "NFT not found."}, status=status.HTTP_404_NOT_FOUND)
