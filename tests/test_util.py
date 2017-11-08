

def cleanup_model(model, using=None):
    if using:
        model.objects.using(using).all().delete()
    else:
        model.objects.all().delete()
