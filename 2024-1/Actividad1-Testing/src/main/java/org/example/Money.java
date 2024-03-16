package org.example;

public class Money {
    private final int amount;
    private final String currency;
    public Money(int amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }
    public int getAmount() {
        return amount;
    }
    public String getCurrency() {
        return currency;
    }
    public boolean equals(Object anObject) {
        if (anObject instanceof Money) {
            Money money = (Money) anObject;
            return getCurrency().equals(money.getCurrency())
                    && getAmount() == money.getAmount();
        }
        return false;
    }

}
