def set_mark(instance, **kwargs):
    instance.sum_of_marks += kwargs['mark']
    instance.amount_of_marks += 1
    instance.current_rating = instance.sum_of_marks / instance.amount_of_marks
