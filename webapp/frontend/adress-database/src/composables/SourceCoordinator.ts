import {ref, watch, onMounted} from 'vue'
import type {Ref} from 'vue'
import { renderToNodeStream } from 'vue/server-renderer'

let coordinator: SourceCoordinator 

export interface Address {
    firstname: string
    lastname: string
    street: string | null
    number: string | null
    zip_code: number | null
    city: string | null
    birthdate: string | null
    phone: string | null
    email: string | null
}

export class SourceCoordinator {
    data: Ref<{ [key: string]: Address } | null>
    private source: null | string 

    setSource(source: null | string) {
        console.log("setSource", source)
        this.source = source
        if (source === "server") {
            console.log("fetch server data")
            this.fetchServerData("server")
        }
    }

    constructor() {
        this.data = ref(null)
        this.source = null
    }

    private fetchServerData(id: string): void {
        fetch(`/api/table/${id}`).then((response) => {
            response.json().then((data) => {
                this.data.value = data
            })
        }).catch((error) => {
            console.log(error)
        })
        return
    }

}
export function useSourceCoordinator(): SourceCoordinator {
    console.log("useSourceCoordinator")
    
    if (!coordinator) {
        coordinator = new SourceCoordinator()
    }
    return coordinator
}

