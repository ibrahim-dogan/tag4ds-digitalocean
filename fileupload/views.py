import json
import random

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from fileupload.models import JsonFile, Tag


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['data']

        json_file = json.loads(uploaded_file.read())
        random.shuffle(json_file)

        file = JsonFile()
        if request.POST['filename']:
            file.name = request.POST['filename'] + '.json'
        else:
            file.name = uploaded_file.name
        file.json = json.dumps(json_file)
        file.row_count = len(json_file)
        file.save()

        return redirect('upload_page')
    else:
        files = JsonFile.objects.order_by('-id')
        context = {'files': files}
        return render(request, 'fileupload/index.html', context)


def prepare_tags(request, id):
    file = get_object_or_404(JsonFile, id=id)
    if file.tags_added:
        return redirect('tag_process', id=id, row=file.index)

    tags = Tag.objects.filter(file=file)
    context = {'tags': tags, 'file': file}
    if request.method == 'POST':
        input_tag = request.POST['tag']
        tag = Tag()
        tag.tag = input_tag
        tag.file = file
        tag.save()
    if request.GET.get('finish'):
        file.tags_added = True
        file.save()
        return redirect('tag_process', id=id, row=file.index)

    return render(request, 'fileupload/prepare_tags.html', context)


def tag_process(request, id, row):
    file = get_object_or_404(JsonFile, id=id)

    if row > file.index or row == file.row_count:
        return redirect('upload_page')

    file_as_json = json.loads(file.json)

    if request.GET.get('tag'):
        tag = get_object_or_404(Tag, id=request.GET.get('tag'), file_id=file.id)
        tag.count = tag.count + 1
        tag.save()

        file_as_json[row]['tag'] = tag.tag

        file.json = json.dumps(file_as_json)
        file.index = file.index + 1 if row >= file.index else file.index
        file.save()
        return redirect('tag_process', id=id, row=file.index)

    tags = Tag.objects.filter(file=file)
    total_count = 0
    for tag in tags:
        total_count = total_count + tag.count
    for tag in tags:
        try:
            tag.percentage = "{0:.2f}".format((tag.count / total_count * 100))
            tag.save()
        except:
            tag.percentage = 0
            tag.save()

    context = {'will_tagged_row': file_as_json[row], 'tags': tags, 'file': file,
               'previous_row': row - 1 if file.index != 0 else 0}
    return render(request, 'fileupload/tag_process.html', context)


def download(request, id):
    file = get_object_or_404(JsonFile, id=id)
    data = []
    for row in json.loads(file.json):
        if 'tag' in row:
            data.append(row)

    data = json.dumps(data, indent=1, ensure_ascii=False)
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=' + file.name
    return response


def download_all(request, id):
    file = get_object_or_404(JsonFile, id=id)
    data = json.loads(file.json)
    data = json.dumps(data, indent=1, ensure_ascii=False)
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=' + 'all_' +file.name
    return response


def validate(request, id):
    file = get_object_or_404(JsonFile, id=id)
    tag_counts = {}
    count = 0
    for row in json.loads(file.json):
        if 'tag' in row:
            count = count + 1
            if row['tag'] in tag_counts:
                tag_counts[row['tag']] = tag_counts[row['tag']] + 1
            else:
                tag_counts[row['tag']] = 0
        else:
            file.index = count
            break

    file.row_count = len(json.loads(file.json))

    file.save()

    tags = Tag.objects.filter(file=file)
    for k, v in tag_counts.items():
        tag = tags.get(tag=k)
        tag.count = v
        tag.save()

    return redirect('upload_page')

    # def prepare_file(request, id):
#     file = get_object_or_404(JsonFile, id=id)
#     file_as_json = json.loads(file.json)
#     first_row = file_as_json[0]
#     first_row_keys = first_row.keys()
#     context = {'file': file, 'first_row': first_row, 'first_row_keys': first_row_keys}
#     if request.method == 'POST':
#         key_list = request.POST.getlist('keys')
#         context['key_list'] = key_list
#
#     return render(request, 'fileupload/prepare.html', context)
