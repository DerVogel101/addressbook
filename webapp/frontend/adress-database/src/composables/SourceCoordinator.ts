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

    // Index signature allowing dynamic access
    [key: string]: any
}

export class SourceCoordinator {
    data: Ref<{ [key: string]: Address } | null>
    private source: null | string 

    setSource(source: null | string) {
        console.log("setSource", source)
        this.source = source
        if (source === "server") {
            console.log("fetch server data")
            this.fetchServerData()
        }
    }

    constructor() {
        this.data = ref(null)
        this.source = null
    }

    private fetchServerData(): void {
        fetch(`/api/table/${this.source}`).then((response) => {
            response.json().then((data) => {
                this.data.value = data
            })
        }).catch((error) => {
            console.log(error)
        })
        return
    }

    public deleateAddress(id: number): void {
        fetch(`/api/edit/${this.source}/${id}`, {
            method: 'DELETE'
        }).then((response) => {
            if (response.ok) {
                this.fetchServerData()
            }
        }).catch((error) => {
            alert(error)
        })
    }

    public addOrUpdate(id: number | undefined, content: Address): void {
        fetch(`/api/edit/${this.source}/${id === undefined ? "" : id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(content)
        }).then((response) => {
            if (response.ok) {
                this.fetchServerData()
            }
        }).catch((error) => {
            alert(error)
        })
    }
}
export function useSourceCoordinator(): SourceCoordinator {
    console.log("useSourceCoordinator")
    
    if (!coordinator) {
        coordinator = new SourceCoordinator()
    }
    return coordinator
}

