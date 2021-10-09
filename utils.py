
from clarifai_grpc.grpc.api import service_pb2, resources_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel

from emoji import emojize
from random import choice
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Start'], 
        ['Rules', 'Dice', 'Gain'],
        ['Pic', 'Questionnaire'],
        [KeyboardButton('Location', request_location=True)]
        ])

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def is_cat(user_photo):
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_json_channel())
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)
    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
        resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(url=user_photo)))
        ])
    response = stub.PostModelOutputs(request, metadata=metadata)  

    if response.status.code != status_code_pb2.SUCCESS:
        print("There was an error with your request!")
        print("\tCode: {}".format(response.outputs[0].status.code))
        print("\tDescription: {}".format(response.outputs[0].status.description))
        print("\tDetails: {}".format(response.outputs[0].status.details))
        raise Exception("Request failed, status code: " + str(response.status.code))
    for concept in response.outputs[0].data.concepts:
        print('%12s: %.2f' % (concept.name, concept.value))
        if concept.name == 'cat':
            return True
        return False
    
if __name__ == "__main__":
    response = is_cat('https://upload.wikimedia.org/wikipedia/commons/7/75/Rana_esculenta_on_Nymphaea_edit.JPG')
    print(response)