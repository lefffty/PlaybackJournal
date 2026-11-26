import {describe, expect, it, jest, beforeEach} from "@jest/globals";
import "@testing-library/jest-dom";
import {render, screen} from "@testing-library/react";
import {MemoryRouter, Route, Routes} from "react-router-dom";

import AxiosInstance from "../AxiosInstance";
import Song from "./Song";

jest.mock("../AxiosInstance");
jest.mock("../Common/ScaleRating/ScaleRating", () => () => (
    <div data-testid="scale-rating">ScaleRating Mock</div>
));

describe("Song component", () => {
    const mockResponse = {
        id: 1,
        cover: "test-image.jpg",
        name: "test-name",
        duration: "00:03:01",
        album: {
            id: 1,
            name: "test-name",
        }
    }

    const renderComponent = (props = {}) => {
        return (
            render(
                <MemoryRouter initialEntries={["/songs/1/"]}>
                    <Routes>
                        <Route path="/songs/:id" element={<Song {...props} />}/>
                    </Routes>
                </MemoryRouter>
            )
        )
    }

    beforeEach(() => {
        jest.clearAllMocks();
        localStorage.clear();
    });

    it('should correctly render information about song if request was successful', async () => {
        AxiosInstance.get.mockResolvedValueOnce({data: mockResponse});

        renderComponent();

        const cover = await screen.findByTestId("song-cover");
        expect(cover).toBeInTheDocument();

        const title = await screen.findByTestId("song-title");
        expect(title).toBeInTheDocument();
        expect(title).toHaveTextContent(mockResponse.name);

        const duration = await screen.findByTestId("song-duration");
        expect(duration).toBeInTheDocument();
        expect(duration).toHaveTextContent(mockResponse.duration);

        const album = await screen.findByTestId("song-album");
        expect(album).toBeInTheDocument();
        expect(album).toHaveTextContent(mockResponse.album.name);
    });

    it('should render error alert if error happened during request', async () => {
        const mockError = new Error("Network error");
        AxiosInstance.get.mockRejectedValueOnce(mockError);

        renderComponent();

        const error = await screen.findByTestId("song-error");
        expect(error).toBeInTheDocument();
        expect(error).toHaveTextContent("Network error");
    });

    it('should render spinner if song was not fetched yet', () => {
        AxiosInstance.get.mockResolvedValueOnce(mockResponse);
        render(<Song/>);

        const spinner = screen.getByTestId("song-spinner");
        expect(spinner).toBeInTheDocument();
    });

    it("omits album link for a single", async () => {
        const newMockResponse = {...mockResponse, album: null};
        AxiosInstance.get.mockResolvedValueOnce({data: newMockResponse});

        renderComponent();

        const album = await screen.queryByTestId("song-album");
        expect(album).not.toBeInTheDocument();
    })

    it('should render scale rating if user is authenticated', async () => {
        localStorage.setItem("auth_token", "1234");
        AxiosInstance.get.mockResolvedValueOnce({data: mockResponse});

        renderComponent();

        const scaleRating = await screen.findByTestId("scale-rating");
        expect(scaleRating).toBeInTheDocument();
    });

    it('should not render scale rating if user is not authenticated', async () => {
        AxiosInstance.get.mockResolvedValueOnce({data: mockResponse});

        renderComponent();

        const scaleRating = screen.queryByTestId("scale-rating");
        expect(scaleRating).not.toBeInTheDocument();
    });
})