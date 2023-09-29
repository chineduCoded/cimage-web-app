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
        getCapturedData: builder.query({
          query: (args) => {
            const {url, selector} = args
            console.log({"args": args})
            return {
              url: `/screenshot?url=${url}&selector=${selector}`
            }
          },
          providesTags: ["Images"]
        }),
        saveScreenshot: builder.mutation({
          query: ({ url, selector }) => ({
            url: "/screenshot",
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ url, selector }),
          }),
          invalidatesTags: ["Images"],
        }),
        getImageId: builder.query({
          query: (imageId) => `/images/${imageId}`,
          providesTags: ["Images"]
        }),
    })
})

export const { useGetCodeQuery, useSaveCodeMutation, useGetCapturedDataQuery, useSaveScreenshotMutation, useGetImageIdQuery } = cimageApi