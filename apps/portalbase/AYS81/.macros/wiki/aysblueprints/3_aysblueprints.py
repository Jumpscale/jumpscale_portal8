

def main(j, args, params, tags, tasklet):
    ayspath = args.getTag('ayspath')
    repo = j.atyourservice.repoGet(ayspath)
    repo._load_blueprints()

    bps = {}
    for blueprint in repo.blueprints:
        bp = dict()
        bp['title'] = blueprint.name
        bp['label_content'] = 'active' if blueprint.active else 'inactive'
        bp['icon'] = 'saved' if not blueprint.active else 'ok'
        bp['label_color'] = 'warning' if not blueprint.active else 'success'
        bp['content'] = j.data.serializer.json.dumps(blueprint.content)
        bps[blueprint.name] = bp

    args.doc.applyTemplate({'data': bps, 'reponame': repo.name})

#     result.append("""
# {{html:
# <script src='/jslib/codemirror/autorefresh.js'></script>
# }}
# {{jscript
#   $(function() {
#       $('.label').click(function() {
#         var that = this
#         var ss = this.id.split('-')
#         var repo = ss.shift()
#         var bp = ss.join('-')
#         if (this.innerText == 'enable'){
#             var url = '/restmachine/ays81/atyourservice/archiveBlueprint';
#         }else{
#             var url = '/restmachine/ays81/atyourservice/restoreBlueprint';
#         }
#         $.ajax({
#           type: 'GET',
#           data: 'repository='+repo+'&blueprint='+bp,
#           success: function(result,status,xhr) {
#             // restore
#             if (that.innerText == 'archived'){
#                 that.classList.remove('glyphicon-saved');
#                 that.classList.remove('label-warning');
#                 that.classList.add('glyphicon-ok');
#                 that.classList.add('label-sucess');
#                 that.innerText = 'enable'
#             }else{ // archive
#                 that.classList.remove('glyphicon-ok');
#                 that.classList.remove('label-sucess');
#                 that.classList.add('label-warning');
#                 that.classList.add('glyphicon-saved');
#                 that.innerText = 'archived'
#             }
#           },
#           error: function(xhr,status,error){ alert('error:'+ error) },
#           url: url,
#           cache:false
#         });
#       });
#     });
# }}
# {{cssstyle
# a.label-archive{
#     color: white;
# }
# }}""")
    # result = '\n'.join(result)

    params.result = (args.doc, args.doc)
    return params
