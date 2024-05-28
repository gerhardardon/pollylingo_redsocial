import { HomeWebPage } from "./views/HomeWebPage"
import { NotFoundPage } from "./views/NotFoundPage"
import { LoginWebPage } from "./views/LoginWebPage";
import { RegisterWebPage } from "./views/RegisterWebPage";

import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
    {
        path: "*",
        element: <NotFoundPage />,
    },
    {
        path: "/",
        element: <HomeWebPage />,
    },
    {
        path: "/login",
        element: <LoginWebPage />,
    },
    {
        path: "/register",
        element: <RegisterWebPage />,
    }
]);


export function Router() {
    return (<RouterProvider router={router} />)
}