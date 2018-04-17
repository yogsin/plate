#!/usr/bin/evn python 
#coding:utf-8 

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
from xml.etree.ElementTree import Comment
from xml.etree.ElementTree import tostring
import os
import sys
import cv2

#create xml structure
def CreateXml(img_name, width, height, depth, object_number, boxes):
  plate = ElementTree()
  annotation = Element("annotation")
  plate._setroot(annotation)
  SubElement(annotation, "folder").text = "plate-private"
  SubElement(annotation, "filename").text = img_name
  source = Element("source")
  SubElement(source, "database").text = "The private Plate Database"
  SubElement(source, "annotation").text = "plate-private"
  SubElement(source, "image").text = "private"
  SubElement(source, "imageid").text = img_name.split('.')[0]
  annotation.append(source)
  owner = Element("owner")
  SubElement(owner,"imageid").text = img_name.split('.')[0]
  SubElement(owner,"name").text = "plate-private"
  annotation.append(owner)
  size = Element("size")
  SubElement(size,"width").text = str(width)
  SubElement(size,"height").text = str(height)
  SubElement(size,"depth").text = str(depth)
  annotation.append(size)
  SubElement(annotation, "segmented").text = "0"
  for i in range(object_number):
      object = Element("object")
      SubElement(object,"name").text = "plate"
      SubElement(object,"pose").text = "Unspecified"
      SubElement(object,"truncated").text = "0"
      SubElement(object,"difficult").text = "0"
      bndbox = Element("bndbox")
      SubElement(bndbox,"xmin").text = str(boxes[i][0])
      SubElement(bndbox,"ymin").text = str(boxes[i][1])
      SubElement(bndbox,"xmax").text = str(boxes[i][2])
      SubElement(bndbox,"ymax").text = str(boxes[i][3])
      object.append(bndbox)
      annotation.append(object)
  indent(annotation)
  return plate

#print xml content
def indent(elem,level=0):
  i ="\n"+level*"  "
  print elem;
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    for e in elem:
      print e
      indent(e,level+1)
    if not e.tail or not e.tail.strip():
      e.tail =i
  if level and (not elem.tail or not elem.tail.strip()):
    elem.tail =i
  return elem

#read the plate annotation file and create correspond xml file
annotation_file = "F:/work/plate/plate-private/ann.txt"
img_path = "F:/work/plate/plate-private/plate/"
xml_path = "F:/work/plate/plate-private/xml/"
with open(annotation_file, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline().strip()
            if not lines:
                break
                pass
            if len(lines.split()) == 2:
                img_name, object_number = lines.split()
                boxes = []
                for i in range(int(object_number)):
                    lines = file_to_read.readline().strip()
                    if not lines and not len(lines.split()) == 4:
                        break
                        pass
                    xmin, ymin, w, h = lines.split()
                    boxes.append([int(xmin), int(ymin), int(xmin) + int(w), int(ymin) + int(h)])
                img_dir = img_path + img_name
                img = cv2.imread(img_dir)
                [height, width, depth] = img.shape
                plate = CreateXml(img_name, width, height, depth, int(object_number), boxes)
                xml_filedir = xml_path + img_name.split('.')[0]
                plate.write(xml_filedir,"utf-8")
            pass
        pass
'''
if __name__ == '__main__':
  plate =CreateXml("0011.jpg", 100, 100, 3, 1, [[2,3,8,9]])
  plate.write(filename,"utf-8")
'''
