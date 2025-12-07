from detection.card_detection import detect_pokemon_card

TEST_CARD_FRONT = "data/raw/199_165_charizard_front.webp"
TEST_CARD_BACK = "data/raw/199_165_charizard_back.webp"
TEST_CARD_FRONT_IVY = "data/raw/167_165_ivysaur_front.webp"
TEST_CARD_FRONT_BULBA = "data/raw/166_165_bulbasaur_front.webp"
TEST_CARD_FRONT_VENU = "data/raw/198_165_venusaur_front.webp"
BULBASAUR_ME_FRONT = "data/raw/133_132_bulbasaur_front.webp"
CHARIZARD_ME_FRONT_1 = "data/raw/154_172_charizard_front.webp"
CHARIZARD_ME_FRONT_2 = "data/raw/174_172_charizard_front.webp"
CHARIZARD_ME_FRONT_SL = "data/raw/199_165_charizard_front_sleeved.webp"
CHARIZARD_ME_FRONT_SWSH = "data/raw/swsh_262_charizard_front.webp"
CHARIZARD_ME_FRONT_3 = "data/raw/234_091_charizard_front.webp"


def main():
    detect_pokemon_card(TEST_CARD_FRONT)
    # detect_pokemon_card(TEST_CARD_BACK)
    # detect_pokemon_card(TEST_CARD_FRONT_IVY)
    # detect_pokemon_card(TEST_CARD_FRONT_BULBA)
    # detect_pokemon_card(TEST_CARD_FRONT_VENU)
    # detect_pokemon_card(BULBASAUR_ME_FRONT)
    # detect_pokemon_card(CHARIZARD_ME_FRONT_SL)
    # detect_pokemon_card(CHARIZARD_ME_FRONT_1)
    # detect_pokemon_card(CHARIZARD_ME_FRONT_2)
    # detect_pokemon_card(CHARIZARD_ME_FRONT_3)
    # detect_pokemon_card(CHARIZARD_ME_FRONT_SWSH)


if __name__ == "__main__":
    main()
