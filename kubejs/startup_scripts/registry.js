
Platform.mods.kubejs.name = "Samgo's Tweaks"

StartupEvents.registry('item', event => {
    event.create('dry_grass')
    .displayName('Dry Grass')

    event.create('tall_dry_grass')
    .displayName('Tall Dry Grass')

    event.create('divine_fragment')
    .displayName('Divine Fragment')
    .rarity('rare')
    .glow(true)

    event.create('divine_favour')
    .displayName('Divine Favour')
    .rarity('rare')
    .glow(true)

    event.create('crystal_heart')
    .displayName('Crystal Heart')
    .fireResistant()
    .unstackable()
    .rarity('rare')
    .glow(true)

    event.create('asylum_seeker')
    .displayName('Asylum Seeker')
    .rarity('rare')
    .unstackable()

    event.create('benzene')
    .displayName('Benzene')

    event.create('wither_heart')
    .displayName("Wither's heart")
    .rarity('epic')
    .unstackable()
    
    event.create('elder_guardian_eye')
    .displayName("Elder Guardian's Eye")
    .unstackable()
    .rarity('rare')

    event.create('warden_heart')
    .displayName("Warden's Heart")
    .unstackable()
    .rarity('epic')

})