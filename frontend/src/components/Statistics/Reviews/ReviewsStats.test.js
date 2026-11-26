import {describe, expect, it} from "@jest/globals";
import "@testing-library/jest-dom";
import {render, screen} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";

import ReviewsStats from "./ReviewsStats";


describe("ReviewsStats component", () => {
    const stats = {
        positive: 6,
        negative: 2,
        neutral: 2,
        total: 10,
    }

    const renderComponent = (props = {}) => {
        return render(
            <MemoryRouter>
                <ReviewsStats
                    stats={stats}
                    {...props}
                />
            </MemoryRouter>
        )
    }

    it('should correctly display main information about reviews stats', () => {
        renderComponent();

        const stats_header = screen.getByTestId("stats-header");
        expect(stats_header).toBeInTheDocument();
        expect(stats_header).toHaveTextContent("Статистика отзывов");

        const stats_total = screen.getByTestId("stats-total");
        expect(stats_total).toBeInTheDocument();
        expect(stats_total).toHaveTextContent("10");

        const stats_positive_label = screen.getByTestId("stats-positive-label");
        expect(stats_positive_label).toBeInTheDocument();
        expect(stats_positive_label).toHaveTextContent("Положительные");

        const stats_positive_amount = screen.getByTestId("stats-positive-amount");
        expect(stats_positive_amount).toBeInTheDocument();
        expect(stats_positive_amount).toHaveTextContent("6");

        const stats_neutral_label = screen.getByTestId("stats-neutral-label");
        expect(stats_neutral_label).toBeInTheDocument();
        expect(stats_neutral_label).toHaveTextContent("Нейтральные");

        const stats_neutral_amount = screen.getByTestId("stats-neutral-amount");
        expect(stats_neutral_amount).toBeInTheDocument();
        expect(stats_neutral_amount).toHaveTextContent("2");

        const stats_negative_label = screen.getByTestId("stats-negative-label");
        expect(stats_negative_label).toBeInTheDocument();
        expect(stats_negative_label).toHaveTextContent("Отрицательные");

        const stats_negative_amount = screen.getByTestId("stats-negative-amount");
        expect(stats_negative_amount).toBeInTheDocument();
        expect(stats_negative_amount).toHaveTextContent("2");
    });

    it('should correctly display review types percentages', () => {
        renderComponent();

        const stats_positive_percentage = screen.getByTestId("stats-positive-percentage");
        expect(stats_positive_percentage).toBeInTheDocument();
        expect(stats_positive_percentage).toHaveTextContent("60.00");

        const stats_neutral_percentage = screen.getByTestId("stats-neutral-percentage");
        expect(stats_neutral_percentage).toBeInTheDocument();
        expect(stats_neutral_percentage).toHaveTextContent("20.00");

        const stats_negative_percentage = screen.getByTestId("stats-negative-percentage");
        expect(stats_negative_percentage).toBeInTheDocument();
        expect(stats_negative_percentage).toHaveTextContent("20.00");
    });
})