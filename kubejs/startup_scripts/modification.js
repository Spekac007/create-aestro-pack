
BlockEvents.modification(event => {
    event.modify('minecraft:furnace', block => {
        block.requiresTool = true;
        block.soundType = 'mud_bricks';
        block.nameKey = 'Mud Kiln';
    })

    event.modify('minecraft:campfire', block => {
        block.nameKey = "Campfire Kindling";
    })  

    event.modify('minecraft:glowstone', block => {
        block.nameKey = "Block of Estus"
    })
})

ItemEvents.modification( event => {
    const stoneToFlint = [
        ['axe', 'Axe'],
        ['hoe', 'Hoe'],
        ['pickaxe', 'Pickaxe'],
        ['shovel', 'Shovel']
    ]
    
    stoneToFlint.forEach(([id, name]) => {
        event.modify(`minecraft:wooden_${id}`, item => {
            item.nameKey = `Flint ${name}`
        })

        event.modify(`minecraft:stone_${id}`, item => {
            item.nameKey = `Copper ${name}`
        })

    })

    event.modify('minecraft:rabbit_hide', item => {
        item.nameKey = 'Tattered Leather'
    })

    event.modify('minecraft:flint_and_steel', item => {
        item.nameKey = 'Fire Striker'
        item.maxDamage = 10
    })

    event.modify('minecraft:ender_pearl', item => {
        item.setMaxStackSize(64)
    })

    event.modify('minecraft:glowstone_dust', item => {
        item.nameKey = 'Estus Ash'
    })

    event.modify('minecraft:enchanted_book', item => {
        item.nameKey = 'Hell-bound Book'
    })

    event.modify('minecraft:blaze_powder', item => {
        item.nameKey = 'Raw Estus'
    })

    event.modify('minecraft:blaze_rod', item => {
        item.nameKey = 'Stabilised Estus'
    })

    event.modify('minecraft:glowstone', item => {
        item.nameKey = "Block Of Estus"
    })

    event.modify('minecraft:chainmail_helmet', item => {
        item.nameKey = 'Copper Helmet'
    })

    event.modify('minecraft:chainmail_chestplate', item => {
        item.nameKey = 'Copper Chestplate'
    })

    event.modify('minecraft:chainmail_leggings', item => {
        item.nameKey = 'Copper Leggings'
    })

    event.modify('minecraft:chainmail_boots', item => {
        item.nameKey = 'Copper Boots'
    })

    event.modify('minecraft:cooked_beef', item => {
        item.nameKey = 'Cooked Beef'
    })
})
