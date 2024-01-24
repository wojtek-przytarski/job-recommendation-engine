import click
from api.client import Client
from recommendations.engine import SpacyRecommendationsEngine, SimpleRecommendationsEngine


def validate_max_delta(ctx, param, value):
    if value < 0:
        raise click.BadParameter('max_delta must be greater than 0')
    if value > 1:
        raise click.BadParameter('max_delta must be less than 1')
    return value


def validate_desired_location_bonus(ctx, param, value):
    if value < 0:
        raise click.BadParameter('desired_location_bonus must be greater than 0')
    if value > 1:
        raise click.BadParameter('desired_location_bonus must be less than 1')
    return value


@click.command()
@click.option('--max-delta', default=0.1, help='Maximum delta compared to highest score for further recommendations.', callback=validate_max_delta, show_default=True)
@click.option('--simple', is_flag=True, help='Use the simple recommendations engine.')
@click.option('--desired-location-bonus', default=0.1, help='Bonus for desired location.', callback=validate_desired_location_bonus, show_default=True)
@click.option('--show-bio', is_flag=True, help='Show candidate bio.')
def main(max_delta, simple, desired_location_bonus, show_bio):
    api_client = Client()
    jobs = api_client.get_jobs()
    candidates = api_client.get_candidates()

    if simple:
        engine = SimpleRecommendationsEngine(jobs, desired_location_bonus=desired_location_bonus)
    else:
        engine = SpacyRecommendationsEngine(jobs, desired_location_bonus=desired_location_bonus)

    for candidate in candidates:
        print(f"Recommendations for {candidate['name']}:")
        if show_bio:
            print(f" Bio: {candidate['bio']}")
        for job in engine.get_recommendations(candidate, max_delta=max_delta):
            print(f" - {job['title']} in {job['location']}")
        print("-------")


if __name__ == '__main__':
    main()
