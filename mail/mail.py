from jinja2 import FileSystemLoader, Environment
import os


data = {"month": None,
        "day": None,
        "format": None,
        "event": None}

for key in data.keys():
    prompt = "Enter the value {}: ".format(key)
    data[key]=input(prompt)

    
top_dir = os.path.abspath(os.path.dirname(__file__))
env = Environment(
    loader=FileSystemLoader(top_dir + "/templates")
)

template = env.get_template("mail.txt")

print(template)

output = template.render(**data)

print("out put template", output)


with open("generate_mail.txt", "w") as _file:
    _file.write(output)

