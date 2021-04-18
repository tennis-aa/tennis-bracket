import os
import jinja2
import sys
import math

def bracketRenderer(bracketSize):
    tournament = "Barcelona 2021"

    rounds = math.log(bracketSize,2)
    if not rounds.is_integer():
            raise ValueError("bracketSize has to be 2^n")
    rounds = int(rounds)

    # input variables
    counter = [0]*(rounds+1)
    for j in range(rounds):
        counter[j+1] = counter[j] + int(bracketSize/(2**j))
    # print(counter)

    render_vars = {"bracketSize" : bracketSize, "rounds" : rounds, "counter" : counter, "tournament": tournament}

    script_path = os.path.dirname(os.path.abspath(__file__))
    # template_file_path = os.path.join(script_path, template_filename)
    
    # Display bracket
    template_filename = "./templateBracketDisplay.jinja"
    fileName="index.html"
    rendered_file_path = os.path.join(script_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # Fillout bracket
    template_filename = "./templateBracketFillout.jinja"
    fileName="submit.html"
    rendered_file_path = os.path.join(script_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # Results bracket
    template_filename = "./templateBracketResults.jinja"
    fileName="inputResults.html"
    rendered_file_path = os.path.join(script_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        bracketSize = int(sys.argv[1])
        bracketRenderer(bracketSize)
    else:
        print("You need to inputs the size of the bracket")
