import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

const baseUrl = "http://127.0.0.1:5000/api/v1"

export const cimageApi = createApi({
    reducerPath: "cimageApi",
    baseQuery: fetchBaseQuery({ baseUrl }),
    tagTypes: ['Images', 'Codes'],
    endpoints: (builder) => ({
        getCode: builder.query({
            query: () => "/",
            providesTags: ['Codes'],
        }),
        saveCode: builder.mutation({
          query: (codeToSave) => ({
            url: "/save-code",
            method: "POST",
            headers: {
              "Content-Type": "text/plain",
            },
            body: codeToSave
          }),
          invalidatesTags: ["Codes"]
        }),
        getScreenshot: builder.query({
          query: ({url, selector}) => ({
            url: `/capture?url=${url}&selector=${selector}`
          }),
          providesTags: ['Images']
        }),
        getImageId: builder.query({
          query: (imageId) => `/images/${imageId}`,
          providesTags: ["Images"]
        }),
    })
})

export const { useGetCodeQuery, useSaveCodeMutation, useGetScreenshotQuery, useGetImageIdQuery } = cimageApi