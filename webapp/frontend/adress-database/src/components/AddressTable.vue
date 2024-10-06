<script setup lang="ts">
import { useSourceCoordinator } from '@/composables/SourceCoordinator'
import { usePopupManager } from '@/composables/PopupManaget';
</script>

<template>
    <div>
        <table>
            <tr>
                <th>id</th>
                <th>firstname</th>
                <th>lastname</th>
                <th>street</th>
                <th>number</th>
                <th>zip_code</th>
                <th>city</th>
                <th>birthdate</th>
                <th>phone</th>
                <th>email</th>
                <th>edit</th>
                <th>delete</th>
            </tr>
            <tr v-for="(address, id) in useSourceCoordinator().data.value">
                <td>{{ id }}</td>
                <td>{{ address.firstname }}</td>
                <td>{{ address.lastname }}</td>
                <td>{{ address.street }}</td>
                <td>{{ address.number }}</td>
                <td>{{ address.zip_code }}</td>
                <td>{{ address.city }}</td>
                <td>{{ address.birthdate }}</td>
                <td>{{ address.phone }}</td>
                <td>{{ address.email }}</td>
                <td><button @click="usePopupManager().editorOpen.value = Number(id)">Edit</button></td>
                <td><button @click="useSourceCoordinator().deleateAddress(Number(id))">Delete</button></td>
            </tr>
        </table>
    </div>

    <div :class="{ 'hidden':  !useSourceCoordinator().data.value}">
        <button @click="usePopupManager().editorOpen.value = true">Add</button>
    </div>
</template>