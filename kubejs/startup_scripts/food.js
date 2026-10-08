const soups = {
    // 16 hunger
    'minecraft:rabbit_stew': 14,

    // 12 hunger
    'minecraft:mushroom_stew': 8,

    // 10 hunger
    'minecraft:beetroot_soup': 8,
    'minecraft:suspicious_stew': 6,
}

const normal = {
    // 6 hunger
    'minecraft:golden_apple': 6,

    // 3 hunger
    'minecraft:baked_potato': 5,
    'minecraft:bread': 4,

    // 2 hunger
    'minecraft:chorus_fruit': 2,
    'minecraft:carrot': 2,
    'minecraft:rotten_flesh': 2,
    'minecraft:honey_bottle': 2,
}

const fast = {
    // 1 hunger
    'minecraft:melon_slice': 1,
    'minecraft:glow_berries': 1,
    'minecraft:sweet_berries': 1,
    'minecraft:beetroot': 1,
    'minecraft:dried_kelp': 1,
    'minecraft:tropical_fish': 1,
    'minecraft:pufferfish': 1,
    'minecraft:poisonous_potato': 1,
    'minecraft:cookie': 1,
    'minecraft:spider_eye': 1,
}

ItemEvents.modification(event => {
    for (const [item, nutrition] of Object.entries(normal)) {
        event.modify(item, item => {
            item.setFood({
                nutrition: nutrition,
                saturation: nutrition * 1.5,
                eatSeconds: 1.6
            })
        })
    }
    for (const [item, nutrition] of Object.entries(soups)) {
        event.modify(item, item => {
            item.setFood({
                nutrition: nutrition,
                saturation: nutrition * 1.5,
                eatSeconds: 3.2,
                usingConvertsTo: 'minecraft:bowl'

            })
        })
    }
    for (const [item, nutrition] of Object.entries(fast)) {
        event.modify(item, item => {
            item.setFood({
                nutrition: nutrition,
                saturation: nutrition * 2.5,
                eatSeconds: 0.8
            })
        })
    }    


})

const tooBigMeat = [
    'minecraft:cooked_beef',
    'minecraft:cooked_porkchop',
    'minecraft:cooked_chicken',
    'minecraft:cooked_mutton',
    'minecraft:cooked_cod',
    'minecraft:cooked_salmon',

    'minecraft:beef',
    'minecraft:porkchop',
    'minecraft:chicken',
    'minecraft:mutton',
    'minecraft:cod',
    'minecraft:salmon',
]

ItemEvents.modification(event => {
    tooBigMeat.forEach(id => {
        event.modify(id, item => {
            item.setFood({
                nutrition: 0,
                eatSeconds: 999,
                saturation: 0
            })
        })
    })
})

