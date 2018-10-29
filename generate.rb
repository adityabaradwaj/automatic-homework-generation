require "erubis"
require "json"

# USAGE: The first argument is "dis" or "hw". The second argument is the number.
#
# This is a Ruby script that generates .tex content files from JSON files.
#
# 1. Read the JSON file, which contains a list of questions.
# 2. From an embedded Ruby file, generate the .tex source file by inserting each question in an "\input{}" command.
# 3. Each template corresponds to one generated .tex file.

type = ARGV[0]
number = ARGV[1]
base_dir = "src/#{type}"

data_file = File.read("#{base_dir}/#{type}#{number}.json")
data_hash = JSON.parse(data_file)

problem_src = "src/problems"
data_hash['questions'].map! {|question| "#{problem_src}/#{question}"}
# raw_questions reads the actual TeX file in order to generate the source TeX file. This is possible because the
# questions and solutions live in separate .tex files now.
raw_questions = data_hash['questions'].map {|question| File.read("#{question}.tex")}

# The suffixes refer to the templates, e.g. "-sol" corresponds to "template-sol.tex.erb". For each of the suffixes
# below, we generate a .tex file from a .tex.erb template.
suffixes = ["", "-sol"]
if type == "hw" or type == "practice"
  # For homeworks, we have another template to generate the raw TeX source file.
  suffixes << "-raw"
end

suffixes.each do |suffix|
  file = "#{base_dir}/template#{suffix}.tex.erb"
  template_file = File.read(file)
  template = Erubis::Eruby.new(template_file)

  # Pass in variables into the templates.
  content = template.result(
    :questions => data_hash['questions'],
    :raw => raw_questions,
    :title => data_hash['title'],
    :date => data_hash['date'],
  )
  File.write("#{base_dir}/#{type}#{number}#{suffix}.tex", content)
end

# This generates one .tex file per question in order to automatically generate images.
if type == "hw"
  file = "#{base_dir}/template-img.tex.erb"
  template_file = File.read(file)
  template = Erubis::Eruby.new(template_file)

  counter = 1
  data_hash['questions'].each do |question|
    content = template.result(:question => question)
    File.write("#{base_dir}/#{type}#{number}-img#{counter}.tex", content)
    counter += 1
  end
end

# TODO:
# Make header and problem titles look like 170
# Incorporate stars for problems
