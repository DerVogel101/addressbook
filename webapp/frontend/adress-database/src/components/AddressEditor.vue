<script setup lang="ts">
import type { Ref } from 'vue'
import type { Address } from '@/composables/SourceCoordinator'
import { ref } from 'vue'
import { useSourceCoordinator } from '@/composables/SourceCoordinator'
import { usePopupManager } from '@/composables/PopupManaget';



const getCurrentValue = (entry: keyof Address): string => {
    if (typeof usePopupManager().editorOpen.value == "number" && useSourceCoordinator().data.value?.[Number(usePopupManager().editorOpen.value)]) {
        return useSourceCoordinator().data.value?.[Number(usePopupManager().editorOpen.value)][entry] ?? ""
    } else {
        return ""
    }
}

function submit(e: Event) {
    e.preventDefault() 
    const formData = new FormData(e.target as HTMLFormElement)
    const address: Address = Object.fromEntries(
        Array.from(formData.entries()).map(([key, value]) => [key, value ? value : null])
    ) as unknown as Address

    useSourceCoordinator().addOrUpdate(typeof usePopupManager().editorOpen.value === "number" ?
        Number(usePopupManager().editorOpen.value) : undefined, address)
    usePopupManager().editorOpen.value = false
}

</script>

<template>
    <div :class="{ 'hidden':  !usePopupManager().editorOpen.value}">
        <h1>Address Editor</h1>
        <form @submit="e => submit(e)">
            <label for="firstname">Firstname</label>
            <input type="text" id="firstname" name="firstname" :value="getCurrentValue('firstname')"/>
            <label for="lastname">Lastname</label>
            <input type="text" id="lastname" name="lastname" :value="getCurrentValue('lastname')"/>
            <label for="street">Street</label>
            <input type="text" id="street" name="street" :value="getCurrentValue('street')"/>
            <label for="number">Number</label>
            <input type="text" id="number" name="number" :value="getCurrentValue('number')"/>
            <label for="zip_code">Zip Code</label>
            <input type="text" id="zip_code" name="zip_code" :value="getCurrentValue('zip_code')"/>
            <label for="city">City</label>
            <input type="text" id="city" name="city" :value="getCurrentValue('city')"/>
            <label for="birthdate">Birthdate</label>
            <input type="text" id="birthdate" name="birthdate" :value="getCurrentValue('birthdate')"/>
            <label for="phone">Phone</label>
            <input type="text" id="phone" name="phone" :value="getCurrentValue('phone')"/>
            <label for="email">E-Mail</label>
            <input type="text" id="email" name="email" :value="getCurrentValue('email')"/>
            <button type="submit">Submit</button>
        </form>
    </div>
</template>