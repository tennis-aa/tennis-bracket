import os
import jinja2
import sys
import math

def bracketRenderer():
    # Parameters
    tournament = "tournament"
    bracketSize = 64
    cellheight = 16 #pixels
    vspace = 2*cellheight
    hspace = 90 #pixels
    linewidth = 1 #pixels


    rounds = math.log(bracketSize,2)
    if not rounds.is_integer():
            raise ValueError("bracketSize has to be 2^n")
    rounds = int(rounds)

    # input variables
    counter = [0]*(rounds+1)
    for j in range(rounds):
        counter[j+1] = counter[j] + int(bracketSize/(2**j))
    # print(counter)

    render_vars = {"bracketSize" : bracketSize, "rounds" : rounds, "counter" : counter, "tournament": tournament,
    "cellheight": cellheight, "vspace": vspace, "hspace": hspace, "linewidth": linewidth}

    script_path = os.path.dirname(os.path.abspath(__file__))
    target_file_path = os.path.join(script_path, "docs" , tournament)
    if not os.path.exists(target_file_path):
        os.mkdir(target_file_path)
    
    # Display bracket
    template_filename = "./templateBracketDisplay.jinja"
    fileName="index.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # Fillout bracket
    template_filename = "./templateBracketFillout.jinja"
    fileName="submit.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # table of positions
    template_filename = "./templateTablePositions.jinja"
    fileName="table.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # Results bracket
    template_filename = "./templateBracketResults.jinja"
    fileName="inputResults.html"
    rendered_file_path = os.path.join(target_file_path, fileName)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    output_text = environment.get_template(template_filename).render(render_vars)
    with open(rendered_file_path, "w") as result_file:
        result_file.write(output_text)

    # Create config.json and players.json templates


if __name__ == "__main__":
    bracketRenderer()

