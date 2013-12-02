import jinja2
import os

with open('toaster_template.xml') as infile:
    template = jinja2.Template(infile.read())

def generate(file):
    im = os.path.splitext(file)[0]
    title = im
    base_url = r'Z:\adsass\toast'
    output_base = base_url
    base_image = file
    output_folder = im

    result = template.render(title=title, base_url=base_url,
                             output_base=output_base,
                             base_image=base_image,
                             output_folder=output_folder)

    with open(im + '.xml', 'w') as outfile:
        outfile.write(result)

def main():
    import sys
    files = [x + '.png' for x in sys.argv[1:]]
    map(generate, files)


if __name__ == "__main__":
    main()
