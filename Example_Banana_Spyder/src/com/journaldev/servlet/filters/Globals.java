package com.journaldev.servlet.filters;

public class Globals {
	private static Globals globalsInstance = new Globals();

    public static Globals getInstance() {
        return globalsInstance;
    }

    private boolean secure = true;

    private Globals() {
    }

    public boolean getsecure() {
        return secure;
    }

}
