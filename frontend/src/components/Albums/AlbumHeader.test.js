import {describe, expect, it, jest} from "@jest/globals";
import AlbumHeader from "./AlbumHeader";
import "@testing-library/jest-dom";
import {render, screen} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";


jest.mock("../Common/ScaleRating/ScaleRating", () => () => (
    <div data-testid="scale-rating">ScaleRating Mock</div>
));
jest.mock("./AlbumActions", () => () => (
    <div data-testid="album-actions">AlbumActions Mock</div>
));


describe("AlbumHeader component", () => {
    const mockAlbum = {
        cover: 'test-cover.jpg',
        name: 'Test Album',
        artists: [
            {id: 1, username: 'Artist 1'},
            {id: 2, username: 'Artist 2'},
        ],
        genres: [
            {id: 1, name: 'Rock'},
            {id: 2, name: 'Pop'},
        ],
        publication_date: '2023-10-15T00:00:00Z',
        average_rating: 8.456,
    };
    const mockUserAlbumData = {rating: 5};
    const mockHandlers = {
        onWishlickClick: jest.fn(),
        onListenedClick: jest.fn(),
        onFavouriteClick: jest.fn(),
        onRatingChange: jest.fn(),
    }

    const renderComponent = (props = {}) => {
        return render(
            <MemoryRouter>
                <AlbumHeader
                    isAuthenticated={true}
                    album={mockAlbum}
                    userAlbumData={mockUserAlbumData}
                    {...mockHandlers}
                    {...props}
                />
            </MemoryRouter>
        )
    }

    it("should display main information about album", () => {
        renderComponent();

        const title = screen.getByTestId("album-title");
        expect(title).toBeInTheDocument();
        expect(title).toHaveTextContent("Test Album");

        const cover = screen.getByTestId("album-cover");
        expect(cover).toBeInTheDocument();

        const artists = screen.getByTestId("album-artists");
        expect(artists).toBeInTheDocument();
        expect(artists).toHaveTextContent("Artist 1, Artist 2");

        const genres = screen.getByTestId("album-genres");
        expect(genres).toBeInTheDocument();
        expect(genres).toHaveTextContent("Rock, Pop");

        const publication_date = screen.getByTestId("album-publication-date");
        expect(publication_date).toBeInTheDocument();
        expect(publication_date).toHaveTextContent("15th October 2023");

        const rating = screen.getByTestId("album-rating");
        expect(rating).toBeInTheDocument();
        expect(rating).toHaveTextContent("8.46");
    });

    it("should correctly render references to artists and genres", () => {
        renderComponent();

        const artist1 = screen.getByText("Artist 1");
        expect(artist1).toHaveAttribute("href", "/artists/1/");
        const artist2 = screen.getByText("Artist 2");
        expect(artist2).toHaveAttribute("href", "/artists/2/");

        const genre1 = screen.getByText("Rock");
        expect(genre1).toHaveAttribute("href", "/genres/1/");
        const genre2 = screen.getByText("Pop");
        expect(genre2).toHaveAttribute("href", "/genres/2/");
    });

    it("should render dash if album average rating is equal to '-'", () => {
        const albumWithDash = { ...mockAlbum, average_rating: '-' };
        renderComponent({ album: albumWithDash });

        const rating = screen.getByTestId("album-rating");
        expect(rating).toHaveTextContent("-");
    });

    it('should always render AlbumActions', () => {
        renderComponent();
        const actions = screen.getByTestId("album-actions");
    });

    it('should render ScaleRating only for authenticated users', () => {
        const {unmount} = renderComponent({isAuthenticated: true});
        var scaleRating = screen.getByTestId("scale-rating");
        expect(scaleRating).toBeInTheDocument();

        unmount();

        renderComponent({ isAuthenticated: false });
        scaleRating = screen.queryByTestId("scale-rating");
        expect(scaleRating).not.toBeInTheDocument();
    });
})