# Backend

Installation

sudo apt-get install python3-pip

pip3 install django

pip3 install django-crispy_forms

pip3 install django-extensions



#Exemplo de card com a propriedade de collapse para a exibição de listas
<div class="card">
  <div class="panel-group">
    {% for group in groups %}
      <div class="panel panel-default">
        <div class="panel-heading">
          <h4 class="panel-title">
            <a data-toggle="collapse" href="#collapse_{{ forloop.counter }}">{{ group.name }}</a>
          </h4>
        </div>
        <div id="collapse_{{ forloop.counter }}" class="panel-collapse collapse">
          <ul class="list-group">
            <li class="list-group-item">{{ group.teacher }}</li>
            <li class="list-group-item">{{ group.creditos }}</li>
            <li class="list-group-item">{{ group.senha_de_acesso }}</li>
          </ul>
        </div>
      </div>
    {% endfor %}
  </div>
</div>
