import { configureStore } from "@reduxjs/toolkit"
import { setupListeners } from "@reduxjs/toolkit/query"
import { cimageApi } from "./api"

export const store = configureStore({
    reducer: {
        [cimageApi.reducerPath]: cimageApi.reducer,
    },

    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(cimageApi.middleware),
})

setupListeners(store.dispatch)