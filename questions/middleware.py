def subscription_processor(request):
    if not 'questions' in request.path or not request.user:
        return {}
    return {
        'current_subscription_question_ids': [subscription.question.id for subscription in Subscription.objects.filter(
            user = request.user,
            ).all()]
    }