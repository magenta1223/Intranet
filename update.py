from task.models import EstimatorType
from task.utils import config_parser
import os

def main():
    types = [t.replace('.json', '') for t in os.listdir('task/configs/')]
    existing_types = [ et.type for et in EstimatorType.objects.all()]
    types = list( set(types) - set(existing_types) )

    if len(types):
        for t in types:
            kwargs, name = config_parser(t)
            e = EstimatorType(type = t, name = name, kwargs = kwargs)
            e.save()
    
        print('Updated')
    
    else:
        print('Already up to date')

main()