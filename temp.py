# import datetime

# from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions


# # connection_string = "DefaultEndpointsProtocol=https;AccountName=crispy0storage0account;AccountKey=+z8Xsc3+o0/0LEslfW/ruQtIOQKhs8f60moQFv7kKP9Ivh9yMyF7dhLJkNf1Zk3qXl9u/WGS4JiB+AStQoyrBw==;EndpointSuffix=core.windows.net"

# account_url = "https://crispy0storage0account.blob.core.windows.net"
# container_name = "cripsy-sentiment-en"
# # blob_name = "221a10e8df9349be9b2632aa62f348cb"
# # sas_token = "sp=r&st=2023-03-27T19:13:54Z&se=2023-03-28T03:13:54Z&spr=https&sv=2021-12-02&sr=b&sig=t46UlhxvPG3VR3XZYpYsUJ%2FZKaxku38UrcVL6OOW4Cc%3D"
# # print(sas_token)


# # blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)

# # # Get a BlobClient object for the blob you want to download
# # blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# # with open("test", "wb") as my_blob:
# #     download_stream = blob_client.download_blob()
# #     my_blob.write(download_stream.readall())


# account_name = "crispy0storage0account"
# account_key = "+z8Xsc3+o0/0LEslfW/ruQtIOQKhs8f60moQFv7kKP9Ivh9yMyF7dhLJkNf1Zk3qXl9u/WGS4JiB+AStQoyrBw=="
# # blob_name = "5120x2880.png"
# blob_name = "Dockerfile"
# # generate_account_sas(account_name=account_name, account_key=account_key)

# permissions = BlobSasPermissions(write=True)
# start_time = datetime.datetime.utcnow()
# expiry_time = start_time + datetime.timedelta(hours=1)

# sas_token = generate_blob_sas(
#     account_name=account_name,
#     container_name=container_name,
#     blob_name=blob_name,
#     account_key=account_key,
#     start=start_time,
#     expiry=expiry_time,
#     permission=permissions
# )

# # print(sas_token)

# # blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)

# # # # Get a BlobClient object for the blob you want to download
# # blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# # # with open("test2", "wb") as my_blob:
# # #     download_stream = blob_client.download_blob()
# # #     my_blob.write(download_stream.readall())

# # with open("Dockerfile", "rb") as my_blob:
#     # blob_client = blob_client.upload_blob(my_blob.read())


# '''
#   For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk
# '''

# # import azure.cognitiveservices.speech as speechsdk

# # # Creates an instance of a speech config with specified subscription key and service region.
# # speech_key = "86f95574c1cb4233a743f7593192eeaa"
# # service_region = "westeurope"

# # speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# # # Note: the voice setting will not overwrite the voice element in input SSML.
# # speech_config.speech_synthesis_voice_name = "en-IN-PrabhatNeural"

# # text = "Positive: It is now past 1 PM and I just finished watching Francis Ford Coppola's 'The Godfather'. I should probably go to bed. It's late and tomorrow I have to wake up a bit early. But not early enough to postpone writing these lines. Now that I have seen it three times, the opportunity of sharing my thoughts and refreshed insights are too much of a good offer to sit on. So, bear with me."

# # # use the default speaker as audio output.
# # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# # result = speech_synthesizer.speak_text_async(text).get()
# # # Check result
# # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
# #     print("Speech synthesized for text [{}]".format(text))
# # elif result.reason == speechsdk.ResultReason.Canceled:
# #     cancellation_details = result.cancellation_details
# #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
# #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
# #         print("Error details: {}".format(cancellation_details.error_details))


# import bcrypt


# def hash_password(password: bytes) -> bytes:
#     return bcrypt.hashpw(password, bcrypt.gensalt())


# def check_password(password: bytes, hashed_password: bytes):
#     return bcrypt.checkpw(password, hashed_password)


# if __name__ == "__main__":
#     test = "test"
#     test_bytes = str.encode(test)
#     print(test_bytes)
#     # hash_test = hash_password(test_bytes)
#     # print(hash_test)

#     hash_test = b'$2b$12$0gs/D8LhSHdhEPAiXMFH0O342L5PaHfjjO6N7bojcVY75/dCoGwWK'

#     print(check_password(test_bytes, hash_test))

#     print(hash_test.decode())

import typing
import base64
import binascii

from pydantic.error_wrappers import ValidationError
from pydantic import BaseModel, EmailStr, validator, root_validator
from pydantic.fields import Field, ModelField

    # @root_validator(pre=True)
    # def parse_token(cls, values: typing.Dict) -> typing.Optional[str]:
    #     print(values)
    #     try:
    #         raw_token = values['authorization']
    #         token_type, token = raw_token.split(" ")
    #         if token_type != "Basic":
    #             raise ValueError('Incorrect token type.')
    #         token_decoded = base64.b64decode(token).decode()
    #         values['email'], values['password'] = token_decoded.split(":")
    #     except (ValueError, binascii.Error) as error:
    #         print(error)
    #         raise ValidationError('Incorrect token.') from error
    #     values['Authorization'] = None
    #     return values



class LoginInputModel(BaseModel):
    authorization: None | str = Field(alias="Authorization", default=None)
    email: None | str = None
    password: None | str = None

    @root_validator(pre=True)
    def parse_token(cls, values: typing.Dict) -> typing.Dict:
        try:
            raw_token = values['Authorization']
            token_type, token = raw_token.split(" ")
            if token_type != "Basic":
                raise ValueError('Incorrect token type.')
            token_decoded = base64.b64decode(token).decode()
            values['email'], values['password'] = token_decoded.split(":")

        except KeyError as error:
            raise ValueError(f'{error} field is required') from error

        except (binascii.Error, ValueError) as error:
            raise ValueError('Incorrect token.') from error

        return values


class RegistrationInputModel(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str = Field(alias="password-repeat")

    @validator("password_repeat")
    def password_match(cls, v: str, values: typing.Dict) -> typing.Optional[str]:
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v



if __name__ == "__main__":
    try:
        t = LoginInputModel()
        print(t.email)
    except ValidationError as err:
        for i in err.errors():
            print(i['msg'])
