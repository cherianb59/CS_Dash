
def add_css_class(class_list, new_class):
  classes = class_list.split(' ')
  if not new_class in classes:
    classes.append(new_class)
  return ' '.join(classes)


def remove_css_class(class_list, class_name):
  return ' '.join([c for c in class_list.split(' ') if c != class_name])
