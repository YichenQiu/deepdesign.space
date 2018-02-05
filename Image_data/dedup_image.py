from PIL import Image
import imagehash
import os
from collections import defaultdict



def dedup_image(directories):
    for label in directories:
        d=defaultdict(list)
        for image in os.listdir('{}'.format(label)):
            if image!=".DS_Store":
                im=Image.open('{}/{}'.format(label,image))
                h=str(imagehash.dhash(im))
                d[h]+=[image]
        lst=[]
        for k,v in d.items():
            if len(v)>1:
                lst.append(list(v))
        for item in lst:
            for image in item [1:]:
                os.unlink("{}/{}".format(label,image))

if __name__=="__main__":
    directories=['Bohemian','Coastal','Industrial','Scandinavian']
    dedup_image(directories)
