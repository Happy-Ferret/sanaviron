#!/usr/bin/python
#-- coding: utf-8 --
import cairo
import math

class Icon():
   def __init__(self, width = 64, height = 64, border = 4):
      self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
      self.context = cairo.Context(self.surface)
      self.draw(self.context, width, height, border)

   def get_filename(self, instance):
      name = str(instance.__class__).split('.')[1]
      filename = "%c" % (ord(name[0]) + 32)
      for byte in list(name[1:]):
         ascii = ord(byte)
         if ascii < 91:
            lower = ascii + 32
            filename += "-%c" % lower
            continue
         filename += byte
      return filename

   def save(self, filename = None):
      if not filename:
         filename = self.get_filename(self)
      filename += ".png"
      with open(filename, "wb") as file:
         self.surface.write_to_png(file)

   def set_color(self, red, green, blue, alpha):
      self.context.set_source_rgba(red / 255.0, green / 255.0, blue / 255.0, alpha / 255.0)

   def draw(self, context, width, height, border):
      raise NotImplementedError

class Rotated():
   def radians(self, degress):
      return degress * math.pi / 180
      
   def rotate(self, context, width, height, angle = 90):
      middle = width / 2
      rotation = self.radians(angle)
      
      context.translate(middle, middle)
      context.rotate(rotation)
      context.translate(-middle, -middle)

class SplitHorizontally(Icon):
   def __init__(self, filename = None):
      Icon.__init__(self)
      self.save(filename)
      
   def draw(self, context, width, height, border):
      middle = width / 2
      separation = 4
      split_height = 6
      arrow_size = 16
      aspect = 6
      
      self.set_color(0, 0, 255, 255)
      context.set_line_width(2)
      
      context.move_to(0, middle)
      context.line_to(width, middle)
      
      context.stroke()
      
      self.set_color(0, 0, 0, 255)
      context.set_line_width(2)
      
      context.move_to(border, middle - separation - split_height)
      context.line_to(border, middle - separation)
      context.line_to(width - border, middle - separation)
      context.line_to(width - border, middle - separation - split_height)
      #---
      context.move_to(border, middle + separation + split_height)
      context.line_to(border, middle + separation)
      context.line_to(width - border, middle + separation)
      context.line_to(width - border, middle + separation + split_height)
      
      context.stroke()

class AddSplitHorizontally(SplitHorizontally):
   def __init__(self, filename = None):
      SplitHorizontally.__init__(self, filename)
      
   def draw(self, context, width, height, border):
      SplitHorizontally.draw(self, context, width, height, border)
      
      middle = width / 2
      separation = 4
      arrow_size = 16
      aspect = 4
            
      self.set_color(70, 160, 70, 255)
      context.set_line_width(2)
      
      context.move_to(middle - arrow_size / 2, middle - separation * 2)
      context.line_to(middle + arrow_size / 2, middle - separation * 2)
      context.line_to(middle, middle - separation - arrow_size - aspect)
      context.close_path()
      #---
      context.move_to(middle - arrow_size / 2, middle + separation * 2)
      context.line_to(middle + arrow_size / 2, middle + separation * 2)
      context.line_to(middle, middle + separation + arrow_size + aspect)
      context.close_path()
      
      context.fill()
      context.stroke()

class AddSplitVertically(AddSplitHorizontally, Rotated):
   def __init__(self, filename = None):
      AddSplitHorizontally.__init__(self, filename)
      
   def draw(self, context, width, height, border):
      Rotated.rotate(self, context, width, height)
      AddSplitHorizontally.draw(self, context, width, height, border)

class RemoveSplitHorizontally(SplitHorizontally):
   def __init__(self, filename = None):
      SplitHorizontally.__init__(self, filename)
      
   def draw(self, context, width, height, border):
      SplitHorizontally.draw(self, context, width, height, border)
      
      middle = width / 2
      size = 16
            
      self.set_color(255, 0, 0, 255)
      context.set_line_width(6)
      context.set_line_cap(cairo.LINE_CAP_ROUND)
      
      context.move_to(middle - size, middle - size)
      context.line_to(middle + size, middle + size)
      #---
      context.move_to(middle + size, middle - size)
      context.line_to(middle - size, middle + size)
      
      context.stroke()

class RemoveSplitVertically(RemoveSplitHorizontally, Rotated):
   def __init__(self, filename = None):
      RemoveSplitHorizontally.__init__(self, filename)
      
   def draw(self, context, width, height, border):
      Rotated.rotate(self, context, width, height)
      RemoveSplitHorizontally.draw(self, context, width, height, border)

class RemoveSplit(RemoveSplitHorizontally, RemoveSplitVertically):
   def __init__(self, filename = None):
      RemoveSplitHorizontally.__init__(self, filename)
      RemoveSplitVertically.__init__(self, filename)
      
   def draw(self, context, width, height, border):
      RemoveSplitHorizontally.draw(self, context, width, height, border)
      RemoveSplitVertically.draw(self, context, width, height, border)

if __name__ == "__main__":
   AddSplitHorizontally("split-horizontally")
   AddSplitVertically("split-vertically")
   RemoveSplit()
