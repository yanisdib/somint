from detection.card_detection import detect_pokemon_card

TEST_CARD_FRONT = "data/raw/199_165_charizard_front.webp"
TEST_CARD_BACK = "data/raw/199_165_charizard_back.webp"
TEST_CARD_FRONT_ALTER = "data/raw/199_165_charizard_front_02.webp"
TEST_CARD_BACK_ALTER = "data/raw/199_165_charizard_back_02.webp"


def main():
    detect_pokemon_card(TEST_CARD_FRONT)
    detect_pokemon_card(TEST_CARD_BACK)
    detect_pokemon_card(TEST_CARD_FRONT_ALTER)
    detect_pokemon_card(TEST_CARD_BACK_ALTER)


if __name__ == "__main__":
    main()
