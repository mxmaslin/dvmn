import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.db.models import F

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.select_related('pokemon'):
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else '',
            'title_ru': pokemon.title
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon_obj = Pokemon.objects.prefetch_related(
            'pokemon_entities'
        ).get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = pokemon_obj.pokemon_entities.select_related('pokemon').all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        add_pokemon(
            folium_map,
            entity.latitude,
            entity.longitude,
            entity.pokemon.title,
            request.build_absolute_uri(
                entity.pokemon.image.url)
        )

    pokemon = {
        'img_url': pokemon_obj.image.url,
        'title_ru': pokemon_obj.title,
        'description': pokemon_obj.description,
        'title_en': pokemon_obj.title_en,
        'title_jp': pokemon_obj.title_jp,
        'previous_evolution': pokemon_obj.previous_evolution,
        'next_evolution': pokemon_obj.next_evolutions.first()
    }
    return render(
        request,
        "pokemon.html",
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon
        }
    )
