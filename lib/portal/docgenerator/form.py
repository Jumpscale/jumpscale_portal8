from JumpScale import j


class Form(object):

    def __init__(self, id, submit_url, submit_method='post', header='', action_button='Confirm',
                 form_layout='', reload_on_success=True, navigateback=False, clearForm=True, showresponse=False):
        self.widgets = []
        self.id = id
        self.form_layout = form_layout
        self.header = header
        self.action_button = action_button
        self.submit_url = submit_url
        self.submit_method = submit_method
        self.showresponse = showresponse
        self.reload_on_success = reload_on_success
        self.navigateback = navigateback
        self.clearForm = clearForm

        import jinja2
        self.jinja = jinja2.Environment(variable_start_string="${", variable_end_string="}")

    def addText(self, label, name, required=False, type='text', value='', placeholder=''):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <input type="${type}" value="${value}", class="form-control" name="${name}" {% if required %}required{% endif %} placeholder="${placeholder}">
              </div>
        ''')
        content = template.render(
            label=label,
            name=name,
            type=type,
            value=value,
            required=required,
            placeholder=placeholder)
        self.widgets.append(content)

    def addHiddenField(self, name, value):
        template = self.jinja.from_string('''
            <input type="hidden" class="form-control" name="${name}" value="${value}">
        ''')
        content = template.render(value=value, name=name)
        self.widgets.append(content)

    def addTextArea(self, label, name, required=False, placeholder=''):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <textarea class="form-control" name="${name}" {% if required %}required{% endif %} placeholder="${placeholder}">
              </div>
        ''')
        content = template.render(label=label, name=name, required=required, placeholder=placeholder)
        self.widgets.append(content)

    def addNumber(self, label, name, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <input type="number" class="form-control" name="${name}" {% if required %}required{% endif %}>
              </div>
        ''')
        content = template.render(label=label, name=name, required=required)
        self.widgets.append(content)

    def addDropdown(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <select class="form-control" name="${name}" {% if required %}required{% endif %}>
                    {% for title, value in options %}
                        <option value="${value}">${title}</option>
                    {% endfor %}
                </select>
              </div>
        ''')
        content = template.render(label=label, name=name, required=required, options=options)
        self.widgets.append(content)

    def addRadio(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height">${label}</label>
                {% for title, value in options %}
                    <label>
                        <input type="radio" name="${name}" value="${value}" {% if required %}required{% endif %}>
                            ${title}
                        </input>
                    </label>
                {% endfor %}
              </div>
        ''')
        content = template.render(label=label, name=name, options=options, required=required)
        self.widgets.append(content)

    def addCheckboxes(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height">${label}</label>
                {% for title, value, checked in options %}
                    <label class="checkbox">
                      <input type="checkbox" {% if checked %}checked{% endif%} {% if required %}required{% endif %} name="${name}" value="${value}" />
                      ${title}
                    </label>
                {% endfor %}
            </div>
        ''')
        content = template.render(label=label, name=name, options=options, required=required)
        self.widgets.append(content)

    def addButton(self, value, type, link=None, id=None):
        tag = 'a' if link else 'button'
        template = self.jinja.from_string('''
        <${tag} type="${type}" class="btn btn-primary" {% if id %}href="${id}"{%endif%} {% if link %}href="${link}"{%endif%}>${value}</${tag}>
        ''')
        content = template.render(type=type, value=value, link=link, tag=tag, id=id)
        self.widgets.append(content)

    def write_html(self, page):
        template = self.jinja.from_string('''
        <form role="form" method="{submit_method}" action="${submit_url}"
        {% for key, value in data.items() -%}
            data-${key}="${value}"
        {%- endfor %}
        >
            <div class="form-group">
                {% for widget in widgets %}${widget}{% endfor %}
             </div>
        </form>
        ''')
        data = {'clearform': j.data.serializer.json.dumps(self.clearForm),
                'reload': j.data.serializer.json.dumps(self.reload_on_success),
                'showresponse': j.data.serializer.json.dumps(self.showresponse),
                'navigateback': j.data.serializer.json.dumps(self.navigateback)}
        content = template.render(id=self.id, header=self.header, action_button=self.action_button, form_layout=self.form_layout,
                                  widgets=self.widgets, submit_url=self.submit_url,
                                  submit_method=self.submit_method, clearForm=self.clearForm, data=data)

        page.addMessage(content)
