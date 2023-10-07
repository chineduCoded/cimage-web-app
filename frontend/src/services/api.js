import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

const baseUrl = "http://127.0.0.1:5000"

export const cimageApi = createApi({
    reducerPath: "cimageApi",
    baseQuery: fetchBaseQuery({ baseUrl }),
    tagTypes: ['Images', 'Codes'],
    endpoints: (builder) => ({
        getCode: builder.query({
            query: () => "/api/v1",
            providesTags: ['Codes'],
        }),
        saveCode: builder.mutation({
          query: (codeToSave) => ({
            url: "/api/v1/save-code",
            method: "POST",
            headers: {
              "Content-Type": "text/plain",
            },
            body: codeToSave
          }),
          invalidatesTags: ["Codes"]
        }),
        getCapturedData: builder.query({
          query: (args) => {
            const {url, selector} = args
            console.log({"args": args})
            return {
              url: "/api/v1/screenshot",
              params: {url, selector}
            }
          },
          providesTags: ["Images"]
        }),
        getImageId: builder.query({
          query: (imageId) => `/api/v1/images/${imageId}`,
          providesTags: ["Images"]
        }),
    })
})

export const { useGetCodeQuery, useSaveCodeMutation, useGetCapturedDataQuery, useGetImageIdQuery } = cimageApi