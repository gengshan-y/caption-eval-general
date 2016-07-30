import hashlib
import io
import sys
import json

class CocoAnnotations:
  def __init__(self):
    self.images = [];
    self.annotations = [];
    self.img_dict = {};
    licenses = [{
                "id" : "text",
                "name" : "test",
                "url" : "test",
                }]
    self.res = {"info" : {},
                "type" : 'captions',  # should keep type as captions [another choice is istances, though I haven't check]
                "images" :  self.images,
                "annotations" : self.annotations,
                "licenses" : licenses,
                }

  
  def get_image_dict(self, img_name):
    image_hash = int(int(hashlib.sha256(img_name).hexdigest(), 16) % sys.maxint)
    if image_hash in self.img_dict:
      assert self.img_dict[image_hash] == img_name, 'hash colision: {0}: {1}'.format(image_hash, img_name)
    else:
      self.img_dict[image_hash] = img_name
    image_dict = {"id" : image_hash,
                "width" : 0,
                "height" : 0,
                "file_name" : img_name,
                "license" : '',
                "url" : img_name,
                "date_captured" : '',
                }
    return image_dict,image_hash

  def read_file(self,filename):
    count = 0
    with open(filename,'r') as opfd:
      for line in opfd:
        count +=1
        id_sent = line.strip()
        sent = id_sent.decode('ascii', 'ignore')
        image_dict,image_hash = self.get_image_dict(str(count))
        self.images.append(image_dict)

        self.annotations.append({
          "id" : len(self.annotations)+1,
          "image_id" : image_hash,
          "caption" : sent,
          })

        if count%1000 == 0:
          print 'Processed %d ...' % count

  def dump_json(self, outfile):
    self.res["images"] = self.images  # should keep it
    self.res["annotations"] = self.annotations
    res = self.res
    with io.open(outfile, 'w', encoding='utf-8') as fd:
      fd.write(unicode(json.dumps(res, ensure_ascii=True,sort_keys=True,indent=2,separators=(',', ': '))))


class CocoResFormat:
  def __init__(self):
    self.res = []
    self.caption_dict = {}

  def read_file(self, filename):
    count = 0
    with open(filename,'r') as opfd:
      for line in opfd:
        count +=1
        id_sent = line.strip()
        sent = id_sent.decode('ascii', 'ignore')
        img_id = int(int(hashlib.sha256(str(count)).hexdigest(), 16) % sys.maxint)
        imgid_sent = {}

        if img_id in self.caption_dict:
          assert self.caption_dict[img_id] == sent
        else:
          self.caption_dict[img_id] = sent
          imgid_sent['image_id'] = img_id
          imgid_sent['caption'] = sent
          self.res.append(imgid_sent)
        if count%1000 == 0:
          print 'Processed %d ...' % count

  def dump_json(self, outfile):
    res = self.res
    with io.open(outfile, 'w', encoding='utf-8') as fd:
      fd.write(unicode(json.dumps(res,
         ensure_ascii=False,sort_keys=True,indent=2,separators=(',', ': '))))
