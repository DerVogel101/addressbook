import { ref } from 'vue'
import type { Ref } from 'vue'
import { onMounted } from 'vue'
interface WindowState {
    editorOpen: Ref<boolean | number>
}

let state: WindowState



export function usePopupManager() {
    if (!state) {
        state = {
            editorOpen: ref(false)
        }
    }

    return state
}