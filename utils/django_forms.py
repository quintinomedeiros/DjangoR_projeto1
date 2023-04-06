from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

# Utilizando os validadores do Django com expressões regulares - lookahead
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$') # Verificação se no campo existe pelo menos uma letra minúscula; pelo menos uma letra maiúscula; e pelo menos um número. ^ e $ indicam que tem que começar e terminar com um destes elementos. Tem que ter no mínimo 8 caracteres e sem máximo.

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='Invalid',
        )
