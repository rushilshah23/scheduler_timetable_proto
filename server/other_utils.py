import os
import json


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)

def save_output_file(file_name, data):

    curr_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(curr_dir, 'outputs')
    file_path = os.path.join(output_dir,file_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # with open(file_path,'w') as json_file:
    #     json.dump(data, json_file,default=lambda obj: obj.to_dict(), indent=4)
    with open(file_path,'w') as fp:
        json.dump(data,fp,cls=CustomEncoder, indent=4)
    