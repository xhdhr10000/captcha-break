from gen.gen_captcha import load_templates, create_captcha
from model.nn import weight_variable
import tensorflow as tf

templates = load_templates()
c,cs = create_captcha(templates)
print(cs)
