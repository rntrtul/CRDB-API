from episodes.models import Episode, Apperance, ApperanceType

epList = Episode.objects.all().order_by("campaign", "num")

cast = ["Grog", "Keyleth", "Percy", "Pike", "Vax'ildan", "Vex'ahlia", "Scanlan", "Tiberius", "Taryon",
        "Fjord", "Beau", "Molly", "Caduceus", "Yasha", "Caleb", "Yasha", "Nott"]

for ep in epList:
    rolls = ep.rolls.all()
    if rolls:
        for roll in rolls:
            appearance = ApperanceType.objects.get(
                name='Cast Member') if roll.character.name in cast else ApperanceType.objects.get(name='Guest')

            app, created = Apperance.objects.update_or_create(character=roll.character, episode=ep, apperance_type=appearance)

            if created:
                print("MADE " + roll.character.name + "IN EP:" + str(ep.num))

    print(ep.title)
