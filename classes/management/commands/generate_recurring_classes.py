from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from classes.models import Class
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Generate recurring classes for the next month"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        today = now.date()

        # Number of days ahead to create
        days_ahead = 30

        # All classes that exist today or previously but should recur
        recurring_classes = Class.objects.filter(start_time__date=today)

        generated_count = 0

        for gym_class in recurring_classes:
            for day in range(1, days_ahead + 1):
                new_start_time = gym_class.start_time + timedelta(days=day * 7)
                new_end_time = gym_class.end_time + timedelta(days=day * 7)

                # Checks if class already exists on date
                if not Class.objects.filter(
                        start_time=new_start_time).exists():
                    try:
                        Class.objects.create(
                            name=gym_class.name,
                            description=gym_class.description,
                            instructor=gym_class.instructor,
                            facility=gym_class.facility,
                            start_time=new_start_time,
                            end_time=new_end_time,
                        )
                        generated_count += 1
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(
                            f"Skipping duplicate: {gym_class.name} "
                            f"on {new_start_time}"))

        self.stdout.write(self.style.SUCCESS(
            f"Successfully generated {generated_count} recurring classes"))
