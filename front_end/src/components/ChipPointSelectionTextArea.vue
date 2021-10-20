<template>
    <div>
        <v-row>
            <v-col
                cols="12"
                sm="1"
            >
                P1 )
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb1x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb1y"
                >
                </v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs1x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs1y"
                >
                </v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col
                cols="12"
                sm="1"
            >
                P2 )
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb2x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb2y"
                >
                </v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs2x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs2y"
                >
                </v-text-field>
            </v-col>
        </v-row>
                <v-row>
            <v-col
                cols="12"
                sm="1"
            >
                P3 )
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb3x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb3y"
                >
                </v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs3x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs3y"
                >
                </v-text-field>
            </v-col>
        </v-row>
                <v-row>
            <v-col
                cols="12"
                sm="1"
            >
                P4 )
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb4x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cb4y"
                >
                </v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs4x"
                >
                </v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="2"
            >
                <v-text-field
                    label="point1"
                    v-model="cs4y"
                >
                </v-text-field>
            </v-col>
        </v-row>
    </div>
</template>

<script>

export default {
    created() {

    },
    mount() {
    
    },
    props: {
        b1x: Number,
        b1y: Number,
        b2x: Number,
        b2y: Number,
        b3x: Number,
        b3y: Number,
        b4x: Number,
        b4y: Number,
        s1x: Number,
        s1y: Number,
        s2x: Number,
        s2y: Number,
        s3x: Number,
        s3y: Number,
        s4x: Number,
        s4y: Number,
    },
    computed: {
        cb1x: {
            get () {
                return this.$props.b1x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cb1y: {
            get () {
                return this.$props.b1y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs1x: {
            get () {
                return this.$props.s1x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs1y: {
            get () {
                return this.$props.s1y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cb2x: {
            get () {
                return this.$props.b2x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cb2y: {
            get () {
                return this.$props.b2y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs2x: {
            get () {
                return this.$props.s2x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs2y: {
            get () {
                return this.$props.s2y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cb3x: {
            get () {
                return this.$props.b3x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cb3y: {
            get () {
                return this.$props.b3y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs3x: {
            get () {
                return this.$props.s3x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs3y: {
            get () {
                return this.$props.s3y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cb4x: {
            get () {
                return this.$props.b4x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cb4y: {
            get () {
                return this.$props.b4y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs4x: {
            get () {
                return this.$props.s4x
            },
            set (value) {
                this.$emit('change', value)
            }
        },
        cs4y: {
            get () {
                return this.$props.s4y
            },
            set (value) {
                this.$emit('change', value)
            }
        },
    },
    components: {

    },
    methods: {

    }
}
</script>

<style scoped>

</style>