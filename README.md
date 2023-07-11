# sorthemall
Sort anything

## Example
```console
$ python sorthemall.py insert 'Buenos días! ¿Cómo está usted?'
Inserted new object with ID: Buenos días! ¿Cómo está usted?

$ python sorthemall.py insert 'Ola ke ase'
Inserted new object with ID: Ola ke ase

$ python sorthemall.py insert 'Hola! ¿Cómo puedo ayudarte?'
Inserted new object with ID: Hola! ¿Cómo puedo ayudarte?

$ python sorthemall.py insert 'Naaaas'
Inserted new object with ID: Naaaas

$ python sorthemall.py auto 'profesionalidad'
task='profesionalidad' oid1='Buenos días! ¿Cómo está usted?' oid2='Ola ke ase' outcome='Buenos días! ¿Cómo está usted?'
task='profesionalidad' oid1='Buenos días! ¿Cómo está usted?' oid2='Hola! ¿Cómo puedo ayudarte?' outcome=None
task='profesionalidad' oid1='Buenos días! ¿Cómo está usted?' oid2='Naaaas' outcome='Buenos días! ¿Cómo está usted?'
task='profesionalidad' oid1='Ola ke ase' oid2='Hola! ¿Cómo puedo ayudarte?' outcome=None
task='profesionalidad' oid1='Ola ke ase' oid2='Naaaas' outcome=None
task='profesionalidad' oid1='Hola! ¿Cómo puedo ayudarte?' oid2='Naaaas' outcome='Hola! ¿Cómo puedo ayudarte?'
Automatically updated ELO scores for all objects and dimensions.

$ python sorthemall.py auto 'amabilidad'
task='amabilidad' oid1='Buenos días! ¿Cómo está usted?' oid2='Ola ke ase' outcome='Buenos días! ¿Cómo está usted?'
task='amabilidad' oid1='Buenos días! ¿Cómo está usted?' oid2='Hola! ¿Cómo puedo ayudarte?' outcome=None
task='amabilidad' oid1='Buenos días! ¿Cómo está usted?' oid2='Naaaas' outcome=None
task='amabilidad' oid1='Ola ke ase' oid2='Hola! ¿Cómo puedo ayudarte?' outcome=None
task='amabilidad' oid1='Ola ke ase' oid2='Naaaas' outcome=None
task='amabilidad' oid1='Hola! ¿Cómo puedo ayudarte?' oid2='Naaaas' outcome='Hola! ¿Cómo puedo ayudarte?'
Automatically updated ELO scores for all objects and dimensions.

$ python sorthemall.py auto 'cercanía'
task='cercanía' oid1='Buenos días! ¿Cómo está usted?' oid2='Ola ke ase' outcome='Buenos días! ¿Cómo está usted?'
task='cercanía' oid1='Buenos días! ¿Cómo está usted?' oid2='Hola! ¿Cómo puedo ayudarte?' outcome=None
task='cercanía' oid1='Buenos días! ¿Cómo está usted?' oid2='Naaaas' outcome='Buenos días! ¿Cómo está usted?'
task='cercanía' oid1='Ola ke ase' oid2='Hola! ¿Cómo puedo ayudarte?' outcome='Ola ke ase'
task='cercanía' oid1='Ola ke ase' oid2='Naaaas' outcome='Naaaas'
task='cercanía' oid1='Hola! ¿Cómo puedo ayudarte?' oid2='Naaaas' outcome='Hola! ¿Cómo puedo ayudarte?'
Automatically updated ELO scores for all objects and dimensions.

$ python sorthemall.py show 'profesionalidad'
Sorted objects by dimension 'profesionalidad':
Buenos días! ¿Cómo está usted?: 1510.5
Hola! ¿Cómo puedo ayudarte?: 1510.5
Ola ke ase: 1500.0
Naaaas: 1489.5

$ python sorthemall.py show 'amabilidad'
Sorted objects by dimension 'amabilidad':
Hola! ¿Cómo puedo ayudarte?: 1510.5
Buenos días! ¿Cómo está usted?: 1500.0
Ola ke ase: 1500.0
Naaaas: 1489.5

$ python sorthemall.py show 'cercanía'
Sorted objects by dimension 'cercanía':
Buenos días! ¿Cómo está usted?: 1510.5
Hola! ¿Cómo puedo ayudarte?: 1510.5
Ola ke ase: 1489.5
Naaaas: 1489.5

```
