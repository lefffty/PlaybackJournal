import {describe, expect, it, jest} from "@jest/globals";
import "@testing-library/jest-dom";
import {render, screen} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";

import AlbumReviews from "./AlbumReviews";


jest.mock("../Reviews/Review", () => () => (
    <div data-testid="review-block">Review</div>
));
jest.mock("../Statistics/Reviews/ReviewsStats", () => () => (
    <div data-testid="reviews-stats">ReviewsStats block</div>
));


describe("AlbumReviews component", () => {
    const reviewsStatistics = {
        total: 10,
        positive: 5,
        negative: 5,
        neutral: 0,
    }
    const reviews = [
        {
            id: 1,
            title: "test title",
            text: "test text",
            reaction: "test like",
            useful_count: 1,
            not_useful_count: 0,
            album: 1,
            type: "negative",
            updated_at: "2023-10-15T00:00:00Z",
            author: {
                avatar: "test-avatar.jpg",
                username: "test username",
            }
        }
    ]

    const renderComponent = (props = {}) => {
        return (
            render(<MemoryRouter>
                <AlbumReviews
                    reviews={reviews}
                    reviewsStatistics={reviewsStatistics}
                    isStatistics={true}
                    id={1}
                    {...props}
                    />
            </MemoryRouter>)
        )
    };

    it('should correctly render components', () => {
       renderComponent();

       expect(screen.getByTestId("reviews-title")).toHaveTextContent("Рецензии слушателей");
    });

    it('should correctly render reviews and reviews stats', () => {
        renderComponent();

        const reviews = screen.getAllByTestId("review-block");
        expect(reviews).toHaveLength(1);
        const reviewsStats = screen.getByTestId("reviews-stats");
        expect(reviewsStats).toBeInTheDocument();
    });

    it('should render null if reviews was not provided', () => {
        renderComponent({isStatistics: false});

        const reviews = screen.queryAllByTestId("review-block");
        expect(reviews).toHaveLength(0);
    });
})