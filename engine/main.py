from detection.card_detection import detect_pokemon_card

TEST_CARD_FRONT = "data/raw/199_165_charizard_front.webp"
TEST_CARD_BACK = "data/raw/199_165_charizard_back.webp"


def main():
    detect_pokemon_card(TEST_CARD_FRONT)


if __name__ == "__main__":
    main()
